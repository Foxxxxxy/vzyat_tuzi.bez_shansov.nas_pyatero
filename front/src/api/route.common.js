export function download_file(url, token, callback = () => { }) {
  let filename = '';
  fetch(url, {
    headers: {
      Authorization: 'Bearer ' + token,
      Accept: '*/*',
      'Content-Type': 'application/json',
    },
    method: 'GET',
  })
    .then((res) => {
      return res.blob();
    })
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a); // append the element to the dom
      a.click();
      a.remove(); // afterwards, remove the element
      callback('done');
    })
    .catch((e) => {
      callback('error');
    });
}

export const changeFiles = (url, e, token) => {
  const files = e.target.files;
  if (!files.length) return;

  e.target.type = 'text'
  e.target.type = 'file'

  return new Promise((resolve, reject) => {
    let file = files[0];
    let formData = new FormData();

    formData.append('file', file);
    fetch(url, {
      headers: {
        Authorization: 'Bearer ' + token,
        Accept: 'application/json',
      },
      method: 'POST',
      body: formData,
    })
      .then((res) => {
        res.json();
      })
      .then((data) => resolve(data))
      .catch((e) => reject(e));
  });
};
