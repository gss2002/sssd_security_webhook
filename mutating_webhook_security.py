from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)

@app.route('/mutate', methods=['POST'])
def mutate():
    request_info = request.get_json()

    # Initialize patch array
    patches = []

    spec = request_info.get('request', {}).get('object', {}).get('spec', {})
    
    # Check and modify securityContext if necessary
    security_context = spec.get('securityContext', {})
    service_account = spec.get('serviceAccount', "")
    service_accountname = spec.get('serviceAccountName', "")

    if 'runAsUser' not in security_context:
       patches.append({
          "op": "add",
          "path": f"/spec/securityContext/runAsUser",
          "value": 1001
       })

    if 'runAsGroup' not in security_context:
       patches.append({
          "op": "add",
          "path": f"/spec/securityContext/runAsGroup",
          "value": 1001
       })
    if 'runAsNonRoot' not in security_context:
       patches.append({
          "op": "add",
          "path": f"/spec/securityContext/runAsNonRoot",
          "value": True
       })
    patches.append({
      "op": "add",
      "path": f"/spec/securityContext/serviceAccount",
      "value": "default"
    })
    patches.append({
      "op": "add",
      "path": f"/spec/securityContext/serviceAccountName",
      "value": "default"
    })

    # Construct the admission review response
    response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
             "uid": request_info.get('request', {}).get('uid'),
             "allowed": True,
             "patchType": "JSONPatch",
             "patch": base64.b64encode(json.dumps(patches).encode()).decode()
        }
    }

    return jsonify(response)

#    except Exception as e:
#        return jsonify({
#            "apiVersion": "admission.k8s.io/v1",
#            "kind": "AdmissionReview",
#            "response": {
#                "allowed": False,
#                "status": {
#                    "message": f"Error processing the request: {str(e)}"
#                }
#            }
#        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/webhook/certs/tls.crt', '/etc/webhook/certs/tls.key'))
