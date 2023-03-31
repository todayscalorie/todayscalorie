function updateStart(uid) {
    let id = uid
    let formData = new FormData()

    formData.append("id_give", id)

    fetch('/admin/updatestart', { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
        alert('업데이트 시작')
        window.location.reload()
    })
}

function updateComplete(uid) {
    let id = uid
    let foodname = $('#' + uid).find('.card-title').text();
    let calorie = $('#' + uid).find('.card-text').text();
    let describe = $('#' + uid).find('.mycomment').text();
    let formData = new FormData()

    formData.append("id_give", id)
    formData.append("foodname_give", foodname)
    formData.append("caloriegive", calorie)
    formData.append("describe_give", describe)

    fetch('/admin/updatecomplete', { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
        alert('업데이트 종료')
        window.location.reload()
    })
}

function deleteCard(uid) {
    let id = uid
    let formData = new FormData()

    formData.append("id_give", id)

    fetch('/admin/delete', { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
        alert('삭제 완료!')
        window.location.reload()
    })
}

function listing() {
    fetch('/admin/get').then(res => res.json()).then(data => {
        let rows = data['result']
        $('#cards-box').empty()
        rows.forEach((a) => {
            let imageurl = a['imageurl']
            let foodname = a['foodname']
            let calorie = a['calorie']
            let describe = a['describe']
            let id = a['id']
            let status = a['status']
            let buttonType
            let buttonText
            let contentEditable

            if (status === "complete") {
                buttonType = "updateStart"
                buttonText = "수정"
                contentEditable = "false"
            } else if (status === "in progress") {
                buttonType = "updateComplete";
                buttonText = "완료"
                contentEditable = "true"
            }
            
            let temp_html = `<div class="col">
                                <div class="card h-100">
                                    <div id="${id}">
                                        <img referrerpolicy="no-referrer" src="${imageurl}" class="card-img-top">
                                        <div class="card-body">
                                            <div id="edit-box" contentEditable="${contentEditable}"> 
                                                <h5 id="test" class="card-title" >${foodname}</h5>
                                            </div>
                                            <div id="edit-box" contentEditable="${contentEditable}">
                                                <p id="test" class="card-text">${calorie}</p>
                                            </div>
                                            <div id="edit-box" contentEditable="${contentEditable}">
                                                <p id="test" class="mycomment">${describe}</p>
                                            </div>
                                            <button id="edit-btn" onclick="${buttonType}('${id}')" type="button" class="btn btn-outline-success btn-sm">${buttonText}</button>
                                            <button onclick="deleteCard('${id}')" type="button" class="btn btn-outline-danger btn-sm">삭제</button>
                                        </div>
                                    </div>
                                </div>
                            </div>`
            $('#cards-box').append(temp_html)
        })
    })
}