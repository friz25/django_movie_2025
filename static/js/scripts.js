function ajaxSend(url, params) {
    // Отправляем запрос
    //*вместо fetch тут можно было исп ajax от jQuery или любой другой библиотеки
    fetch( input: `${url}?${params}`, init:{
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })Promise<Response>
        .then(response => response.json())Promise<any>
        .then(json => render(json))Promise<void>
        .catch(error => console.error(error))
}

const forms = document.querySelector( selectors: 'form[name=filter]');

forms.addEventListener(type:'submit', listener: function(e:Event) {
    // Получаем данные из формы
    e.preventDefault(); // блокирует default действие (обновление страницы)
    let url = this.action;
    let params = new URLSearchParams(new FormData(this)).toString();
    ajaxSend(url, params);
});

function render(data) {
    // Рендер шаблона
    let template = Hogan.compile(html);
    let output = template.render(data);

    const div = document.querySelector(selectors:'.left-ads-display>row');
    div.innerHTML = output;
}

let html = '\
{{#movies}}\
    <div class="col-md-4 product-men">\
        <div class ="product-shoe-info editContent text-center mt-lg-4">\
            <div class="men-thumb-item">\
                <img src="media/{{ poster }}" class="img-fluid" alt="">\
            </div>
            <div class="item-info-product">\
                <h4 class="">\
                    <a href="/{{ url }}" class="editContent">{{ title }}</a>\
                </h4>
                <div class="product_price">\
                    <div class="grid-price">\
                        <span class="money editContent">{{ tagline }}</span>\
                    </div>\
                </div>\
                <ul class="stars">\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                </ul>\
            </div>\
        </div>\
    </div>\
{{/movies}}'


'
