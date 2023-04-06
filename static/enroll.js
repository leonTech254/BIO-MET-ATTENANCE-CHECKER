const fileInput = document.getElementById('file-input');
const previewDiv = document.querySelector('.preview-image');

fileInput.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(event) {
      const img = document.createElement('img');
      
    img.src = event.target.result;
      previewDiv.innerHTML = '';
    previewDiv.appendChild(img);
  }

  reader.readAsDataURL(file);
});


let message = document.getElementById("message")
let button = document.getElementById("btn").addEventListener('click', (e) => {
  EnrollUsers(e)
   
 })

     
        function EnrollUsers(event)
        {
           event.preventDefault();
  let lname = document.getElementById("lname").value;
  let fname = document.getElementById("fname").value;
  let mname = document.getElementById("mname").value;
  let email = document.getElementById("email").value;
  let fileInput = document.getElementById("file-input");
  
  let data = new FormData();
  data.append('lname', lname);
  data.append('fname', fname);
  data.append('mname', mname);
  data.append('email', email);
  if (fileInput.files.length > 0) {
    let file = fileInput.files[0];
    data.append('image', file, file.name);
  }

  axios.post("http://127.0.0.1:5000/api/register", data)
    .then((res) => {
      console.log(res.data);
      // alert(res.data);
    })
    .catch((err) => {
      console.error(err);
      alert("Error occurred");
    });
        }
        