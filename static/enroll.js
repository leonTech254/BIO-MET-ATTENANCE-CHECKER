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


 let message=document.getElementById("message")

        var socket = io.connect("http://192.168.43.225:5000");
        socket.on('connect', function () {
            socket.emit('my event', { data: 'I\'m connected!' });
        });
        function EnrollUsers()
        {
         
            let lname = document.getElementById("lname").value;
            let fname = document.getElementById("fname").value;
            let mname = document.getElementById("mname").value;
            let email = document.getElementById("email").value;
            let data_array = [lname, fname, mname, email]
            let checker = true;
            for (let i = 0; i < data_array.length; i++)
            {
                if (data_array[i] == "")
                {
                    checker = false;
                    alert('all field required');
                    break;
                }
                
            }
            if (checker)
            {
               const file = fileInput.files[0];
  
  const reader = new FileReader();
  reader.addEventListener('load', (event) => {
    const imageData = event.target.result;
    
    let data={'lname':lname,'fname':fname,'mname':mname,'email':email,"image": imageData}
    socket.emit("from_flask",{"credentials":data})
  });
  
  reader.readAsDataURL(file);
          
                
           
            }

        }
         socket.on("name", (data) => {
           alert(data.message)
           

            })