/**
 * 함수, 변수 위로 달리는 \/***\/ 형태 주석의 장점은
 * 해당 함수를 사용할 때 어떤 함수인 지를 알 수 있다는 점이 있습니다.
 * 
 * 업데이트 시작 정보 저장
 * @param {string} uid 음식 게시물의 objectId
 */
async function updateStart(uid) { // async는 해당 함수를 비동기로 만들어 줍니다.
    const id = uid // 수정되지 않는 값은 const로 선언
    
    const formData = new FormData()
    formData.append("id_give", id)
    console.log(`[ POST /admin/updatestart ] REQUEST`)
    // await는 비동기 함수 내에서 동기로 처리되어야 하는 부분에 사용됩니다! 
    const response = await fetch('/admin/updatestart', { method: "POST", body: formData })
    const responseBody = await response.json()
    // JSON.stringify -> json 타입(js의 유사 type은 Object type)을 문자열 형태로 변환합니다.)
    console.log(`[ POST /admin/updatestart ] RESPONSE - body: ${JSON.stringify(responseBody)}`)
    alert('업데이트 시작')
    window.location.reload()
}

/**
 * 업데이트 완료
 * @param {string} uid 음식 게시물의 objectId
 */
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
    fetch('/admin').then(res => res.json()).then(data => {
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