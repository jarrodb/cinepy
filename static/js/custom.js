function update_form_with_object(form, obj, pfx) {
    form_array = form.find("select, textarea, input").serializeArray();
    $.each(form_array, function() {
        var el_name = this['name'];
        var obj_name = el_name;
        if (pfx) {
            // strip the pfx
            obj_name = el_name.replace(pfx, "");
        }
        if (obj_name in obj) {
            var el = form.find("[name="+el_name+"]");
            el.val(obj[obj_name]);
        }
    });
}
function meta_data_for_title(form_id, title, field_prefix) {
    if (!field_prefix) {
        field_prefix="";
    }
    $.ajax({
        type:"get",
        url:"/api/movie/meta",
        data:"title="+title,
        dataType: "json",
        timeout: 3000,
        beforeSend: function() {
            // save for placing it all back?
            var orig_data = $("#"+form_id).serializeArray();
        },
        success: function(msg) {
            var movieform = $('#'+form_id);
            update_form_with_object(movieform, msg, field_prefix);
            // IMDb does not allow hot-linking -- ugh
            //if ('poster_url' in msg) {
            //    poster_el = $('#'+field_prefix+'poster_url');
            //    if (msg['poster_url']) {
            //        poster_el.attr("src",msg['poster_url']);
            //    }
            //}
            return false;
        },
    });
}
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
function movie_time(url, movie_id, time) {
    $.ajax({
        type:"post",
        url:url,
        data:"movie_id="+movie_id+"&time="+time+"&_xsrf="+getCookie("_xsrf"),
        dataType:"json",
        timeout: 2000,
        success: function(msg) {
            if (msg['success']) {
                // yay
            } else {
                // nay
            }
        },
    });
};
function queue(url, movie_id, form_type) {
    form_type = typeof form_type !== 'undefined' ? form_type : "post";
    $.ajax({
        type:form_type,
        url:url,
        data:"movie_id="+movie_id+"&_xsrf="+getCookie("_xsrf"),
        dataType:"json",
        timeout: 2000,
        success: function(msg) {
            if (msg['success']) {
                alert("position: " + msg['position']);
                // yay
            } else {
                // nay
            }
        },
    });
    return false;
};
