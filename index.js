replaceImage(document.images)



async function replaceImage(element){

for (var i = 0; i < element.length; i++) {
	let what = await fetch('http://127.0.0.1:5000/', {method: 'POST', headers: {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'
  },body:  JSON.stringify(element[i].getAttribute("src"))})
let commit = await what.json()
element[i].src = commit['image']
console.log('hehe')
}
}
