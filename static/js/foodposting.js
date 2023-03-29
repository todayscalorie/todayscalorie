function posting() {
    let imageurl = $('#imageurl').val()
    let foodname = $('#foodname').val()
    let calorie = $('#calorie').val()
    let describe = $('#describe').val()
    let formData = new FormData()
    let imagecheck

    formData.append("imageurl_give", imageurl)

    fetch('/admin/imagecheck', { method: "POST", body: formData }).then(res => res.json()).then(data => {
        console.log(data)
        if (data['status'] == "True") {
            console.log("a")
            imagecheck = data.status
            console.log(imagecheck)
        } else {
            console.log("b")
            imagecheck = data.status
            console.log("e")
        }
    })
    console.log("c"+imagecheck)

    if (imagecheck === "True") {
        formData.append("foodname_give", foodname)
        formData.append("calorie_give", calorie)
        formData.append("describe_give", describe)

        fetch('/admin', { method: "POST", body: formData }).then(res => res.json()).then(data => {
            alert(data['msg'])
            window.location.reload()
        })
    } else {
        alert("이미지가 아닙니다.")
        return;
    } 
}