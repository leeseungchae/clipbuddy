async function sendVideo() {
    const fileInput = document.getElementById('pc-upload-add');
    const file = fileInput.files[0];

    if(file == undefined){
      alert('파일을 입력해 주세요.')
      return false;
    }

    const formData = new FormData();
    formData.append('file', file);

    // 그리고 로딩창을 켜줘야 함
    $('.loader-hidden').addClass('loader-visible')
    $('.loader-visible').removeClass('loader-hidden')


    const response = await fetch('http://localhost:8000/upload-video', {
      method: 'POST',
      body: formData,
      // credentials: 'include' // 쿠키를 포함하여 요청
    })
    .then(async(response)=>{
      if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem('user_id', data.user_id);
        location.replace('chatbotPage.html');
      } else {
        console.log('File upload failed');
        const errorMessage = await response.text(); // 또는 response.json() 사용
        console.log('Error:', errorMessage);
        alert('파일 업로드에 실패하였습니다.');
  
          // 그리고 로딩창을 켜줘야 함
        $('.').addClass('loader-hidden')
        $('.loader-hidden').removeClass('loader-visible')
          return false;
      }
    })
    .catch(() => {
      console.log('File upload failed');
      alert('파일 업로드에 실패하였습니다.')

        // 그리고 로딩창을 켜줘야 함
      $('.loader-visible').addClass('loader-hidden')
      $('.loader-hidden').removeClass('loader-visible')
        return false;
    });

}


function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
  // console.log('Current cookies:', document.cookie);
}