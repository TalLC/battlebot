let baseHeaders = new Headers();
baseHeaders.append("Content-Type", "application/json");

let requestOptions = {
  headers: baseHeaders,
  redirect: 'follow'
};

export default function sendRestMessage(method, endpoint, content){
    requestOptions.method = method;
    requestOptions.body = JSON.stringify(content);
    fetch(endpoint, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}
