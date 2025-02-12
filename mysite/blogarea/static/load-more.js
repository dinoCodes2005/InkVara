$(document).ready(function () {
  $("#load-more").on("click", function () {
    var _currentResult = $(".blog-cards").length;
    console.log("Current Result : " + _currentResult);
    $.ajax({
      url: "{% url 'load-more' %}",
      type: "POST",
      data: {
        offset: _currentResult,
        csrfmiddlewaretoken: "{{csrf_token}}",
      },
      dataType: "json",
      beforeSend: function () {
        $("#load-more").addClass("disabled").text("Loading.....");
      },
      success: function (res) {
        console.log(res);
        var _html = "";
        var json_data = $.parseJSON(res.posts);
        console.log("JSON DATA : " + JSON.parse(res.posts));
        $.each(json_data, function (index, data) {
          _html += `
                <div class="blog-cards">
                <a href="javascript:void(0)">
                  <div class="relative flex flex-col my-1 bg-white shadow-sm border border-slate-200 rounded-lg w-96">
                    <div class="relative h-56 overflow-hidden text-white rounded-md">
                      <img src="/media/${data.fields.thumbnail}" alt="card-image" class="object-cover w-full h-full" />
                    </div>
                    <div class="p-4">
                      <h6 class="mb-2 text-slate-800 text-xl font-semibold">${data.fields.title}</h6>
                      <p class="text-slate-600 leading-normal font-light">${data.fields.articleSnippet}</p>
                    </div>
                    <div class="flex items-center justify-between p-4">
                      <div class="flex items-center">
                        <img alt="${data.fields.author}" src="/media/${data.fields.author.profileImage}" class="relative inline-block h-8 w-8 rounded-full" />
                        <div class="flex flex-col ml-3 text-sm">
                          <span class="text-slate-800 font-semibold">${data.fields.author}</span>
                          <span class="text-slate-600">${data.fields.date}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </a>
                </div>`;
        });
        $("#cardContainer").append(_html);
        var _countTotal = $(".blog-cards").length;
        console.log("Count Total : " + _countTotal);
        if (_countTotal == res.totalResult) {
          $("#load-more").remove();
        } else {
          $("#load-more").removeClass("disabled").text("Load More");
        }
      },
    });
  });
});
