function listing() {
    fetch('/admin').then(res => res.json()).then(data => {
        let rows = data['result']
        $('#cards-box').empty()
        rows.forEach((a) => {
            let imageurl = a['imageurl']
            let foodname = a['foodname']
            let calorie = a['calorie']
            let describe = a['describe']

            let temp_html = `<div class="col">
                                <div class="card h-100">
                                    <img referrerpolicy="no-referrer" src="${imageurl}" class="card-img-top">
                                    <div class="card-body">
                                        <h5 class="card-title">${foodname}</h5>
                                        <p class="card-text">${calorie} kcal</p>
                                        <p class="mycomment">${describe}</p>
                                    </div>
                                </div>
                            </div>`

            $('#cards-box').append(temp_html)
        })
    })
}