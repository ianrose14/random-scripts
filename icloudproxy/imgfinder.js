
var lastImgUrl = '';
var changes = [];

function dl(u) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState === 4) {
      console.log('ok!');
    }
  };
  xhr.open('GET', 'http://localhost:9933?q=' + encodeURIComponent(u), true);
  xhr.send(null);  // No data needs to be sent along with the request.
}

function checkImgUrl() {
  var container = document.getElementById('View68');
  var children = container.childNodes;

  for (var i=1; i < children.length; i++) {
    if (children[i-1].getAttribute('id') == 'View75') {
      var subj = children[i];
      var imgs = subj.getElementsByTagName('img');
      if (imgs.length == 1) {
        var src = imgs[0].getAttribute('src');
        if (src != lastImgUrl) {
          console.log('new image!!  ' + src);
          dl(src);
          lastImgUrl = src;
          changes.push(src);
        }
      }
    }
  }
}

function dump() {
  var e = document.createElement('span');
  var s = '';
  changes.forEach(function(e) { s = e + '\n'; });
  e.innerText = s;
  //changes.forEach(function(e) { console.log('go_' + e); });
}

window.setInterval(checkImgUrl, 100);
