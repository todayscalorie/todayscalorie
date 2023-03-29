function posting() {
    let imageurl = $('#imageurl').val()
    let foodname = $('#foodname').val()
    let calorie = $('#calorie').val()
    let describe = $('#describe').val()
    let formData = new FormData()

    formData.append("imageurl_give", imageurl)

    fetch('/admin/imagecheck', { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            if (data['status'] == "True") {
                console.log("a")
                imagecheck = data.status
                console.log(imagecheck)

                formData.append("foodname_give", foodname)
                formData.append("calorie_give", calorie)
                formData.append("describe_give", describe)

                fetch('/admin', { method: "POST", body: formData })
                    .then(res => res.json())
                    .then(data => {
                        alert(data['msg'])
                        window.location.reload()
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            } else {
                console.log("b")
                imagecheck = data.status
                console.log("e")
                alert("이미지가 아닙니다.")
            }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}