function caclKcal(calorie, uid) {
    const resultElement = document.getElementById(uid).querySelector('#result');
    const calcresultElement = document.getElementById(uid).querySelector('#calcresult');
    let number = resultElement.innerText;
    let kcal = calorie

    result = parseInt(number) * parseInt(kcal)

    calcresultElement.innerText = result;
}

function count(type, uid)  {
    const resultElement = document.getElementById(uid).querySelector('#result');
    let number = resultElement.innerText;
    
    // 더하기/빼기
    if(type === 'plus') {
      number = parseInt(number) + 1;
    }else if(type === 'minus')  {
      number = parseInt(number) - 1;
    }

    // 0 아래로 내려가면 0으로 반환
    if (number === -1) {
        number = 0
    }
    
    // 결과 출력
    resultElement.innerText = number;
}

function foodlist() {
  fetch("/get")
    .then((res) => res.json())
    .then((data) => {
      let rows = data["result"];
      $("#cards-box").empty();
      rows.forEach((a) => {
        let imageurl = a["imageurl"];
        let foodname = a["foodname"];
        let calorie = a["calorie"];
        let id = a["id"];

        let temp_html = `<div class="col" id="${id}">
                                <div class="card h-100">
                                    <h3 class="card-header">${foodname}</h3>
                                    <img referrerpolicy="no-referrer" src="${imageurl}" class="card-img-top">
                            
                                    <div class="card-body">
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" />
                                            <label class="form-check-label" for="flexCheckDefault">
                                                ${foodname}
                                            </label>
                                        </div>
                                    </div>

                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item">칼로리 : ${calorie} (100g)</li>
                                            <li class="list-group-item">
                                            먹은 양 체크
                                            <div class="d-flex justify-content-between">
                                                <button onclick="count('minus','${id}')" value="-" "type="button" class="btn btn-outline-dark">-</button>
                                                <div id="result">0</div>
                                                <button onclick="count('plus','${id}')" value="+" "type="button" class="btn btn-outline-dark">+</button>
                                            </div>
                                        </li>
                                    </ul>
                                    <div class="card-body">
                                        <button onclick="caclKcal('${calorie}','${id}')" type="button" class="btn btn-outline-success">
                                            칼로리계산하기
                                        </button>
                                        <div id="calcresult"></div>
                                    </div>
                                </div>
                            </div>`;
        $("#cards-box").append(temp_html);
      });
    });
}


