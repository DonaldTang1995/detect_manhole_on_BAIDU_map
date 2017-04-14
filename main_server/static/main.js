var server_url = "/UCS";
map = new BMap.Map("container");
all_images = new Array({ 'bounding_box': new Array([297, 246, 369, 284, 0.824773]), 'lat': 40.0030547684, 'long': 116.474414025, 'url': 'http://api.map.baidu.com/panorama/v2?ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb&width=1000&height=512&location=116.474414,40.003055&fov=120&pitch=40&heading=90' });
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
var get_rect;
var get_point;
function draw_rect() {

    min_lng = null, min_lat = null, max_lng = null, max_lat = null;
    get_rect = function (e) {
        var pt = new BMap.Point(e.point.lng, e.point.lat);
        var myIcon = new BMap.Icon("/static/img/dot.png", new BMap.Size(6, 6));
        if (min_lng == null) {
            marker1 = new BMap.Marker(pt, { icon: myIcon });
            map.addOverlay(marker1);
            min_lat = e.point.lat;
            min_lng = e.point.lng;
        }
        else {
            marker2 = new BMap.Marker(pt, { icon: myIcon });
            map.addOverlay(marker2);
            max_lat = e.point.lat;
            max_lng = e.point.lng;
            if (min_lat > max_lat) {
                [min_lat, max_lat] = [max_lat, min_lat];
            }
            if (min_lng > max_lng) {
                [min_lng, max_lng] = [max_lng, min_lng];
            }

            polygon = new BMap.Polygon([
                new BMap.Point(min_lng, min_lat),
                new BMap.Point(min_lng, max_lat),
                new BMap.Point(max_lng, max_lat),
                new BMap.Point(max_lng, min_lat)
            ], { strokeColor: "blue", strokeWeight: 6, strokeOpacity: 0.5 });
            map.addOverlay(polygon);
            $('#searching_window, #overlay-back').fadeIn(500);
            $('#search_by_name').on('click', { min_lng, min_lat, max_lng, max_lat }, search_by_name);
        }
    }
    map.addEventListener("click", get_rect);
}

function search_coordinate() {
    remove_all_listener();
    get_point = function (e) {
        var lat = e.point.lat, lng = e.point.lng;
        var url = "http://api.map.baidu.com/panorama/v2?ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb&width=1000&height=512&location=" + lng + "," + lat + "&fov=120&pitch=40&heading=90";
        var image = { "bounding_box": [], "lat": lat, "long": lng, "url": url };
        add_marker(image);
        map.removeEventListener("click", get_point);
    }
    map.addEventListener("click", get_point);
}

function remove_all_listener() {
    map.removeEventListener("click", get_rect);
    map.removeEventListener("click", get_point);
}

function close_searching_window() {
    min_lng = null, min_lat = null, max_lng = null, max_lat = null;
    map.removeEventListener("click", get_rect);
    map.removeOverlay(marker1);
    map.removeOverlay(marker2);
    map.removeOverlay(polygon);
    $("#image_analysis").attr("disabled", true);
    $('#searching_window, #overlay-back').fadeOut(500);
}

function close_image_window() {
    $('#image_window, #overlay-back').fadeOut(500);
}

function search_by_name() {
    var placename = jQuery("#placename").val();
    if (placename == "") {
        alert("Place name must be specified");
        return;
    }
    $('body').addClass("loading");
    jQuery.ajax({
        type: "POST",
        url: server_url,
        data: JSON.stringify({
            'token': getCookie('token'),
            "command": "search_by_name",
            'max_long': max_lng,
            'min_long': min_lng,
            'max_lat': max_lat,
            'min_lat': min_lat,
            'placename': placename
        }),
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                var lat = data[i].latitude, lng = data[i].longitude;
                var url = "http://api.map.baidu.com/panorama/v2?ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb&width=1000&height=512&location=" + lng + "," + lat + "&fov=120&pitch=40&heading=90";
                var image = { "bounding_box": [], "lat": lat, "long": lng, "url": url };
                add_marker(image);
            }
            $('body').removeClass("loading");
            //alert(data);
            //alert(obj.contry.area.women);
        },
        error: function (x) {
            console.log(x);
            $('body').removeClass("loading");
            alert(x.responseText);
        },
        dataType: 'json'
    });
}
function search_bounding_box() {
    $('body').addClass("loading");
    jQuery.ajax({
        type: "POST",
        url: server_url,
        data: JSON.stringify({
            'token': getCookie('token'),
            "command": "search_bounding_box",
            'max_long': max_lng,
            'min_long': min_lng,
            'max_lat': max_lat,
            'min_lat': min_lat
        }),
        success: function (data) {
            $('body').removeClass("loading");
            $("#image_analysis").removeAttr("disabled");
            alert("Find " + data + " images");
            setCookie("image_num",data);
            //alert(data);
            //alert(obj.contry.area.women);
        },
        error: function (x) {
            console.log(x);
            $('body').removeClass("loading");
            alert(x.responseText)
        },
        dataType: 'json'
    });
}

function display_one_image(image) {

    const draw = (ctx, x, y, w, h, score, c) => {
        ctx.beginPath();
        ctx.rect(x, y, w, h);
        ctx.strokeStyle = c;
        ctx.stroke();
        ctx.font = '15px serif';
        ctx.fillText(score, x, y - 5);
    };
    var canvas_ = jQuery('#image');
    canvas_.data("position", { lat: image.lat, long: image.long });
    var ctx = canvas_[0].getContext('2d');
    var img = new Image();
    img.crossOrigin = "Anonymous";
    bounding_boxes = image.bounding_box;
    img.onload = function () {
        ctx.drawImage(img, 0, 0);
        for (i = 0; i < bounding_boxes.length; i++) {
            [xmin, ymin, xmax, ymax, score] = bounding_boxes[i];
            draw(ctx, xmin, ymin, xmax - xmin, ymax - ymin, score, 'red');
        }
        $('#image_window, #overlay-back').fadeIn(500);
    }
    img.src = "/image/" + encodeURIComponent(image.url);
}

function add_marker(image) {
    var lat = image.lat;
    var long = image.long;
    var marker = new BMap.Marker(new BMap.Point(long, lat));
    marker.addEventListener("click", function () {
        display_one_image(image);
    });
    var removeMarker = function (e, ee, marker) {
        map.removeOverlay(marker);
    }
    var markerMenu = new BMap.ContextMenu();
    markerMenu.addItem(new BMap.MenuItem('delete', removeMarker.bind(marker)));
    marker.addContextMenu(markerMenu)
    map.addOverlay(marker);
}

function display_images(images) {
    for (i = 0; i < images.length; i++) {
        (function (ii) {
            add_marker(images[ii]);
        })(i);
    }
}

function image_analysis() {
    var object_name = jQuery('#object').find(":selected").text();
    var image_num = getCookie('image_num');
    var percent_val = '0%';
    $('#percent').text(percent_val);
    var batch = Math.max(20, image_num / 100);
    $('body').addClass("processing");
    var max_iter = image_num / batch;
    function request(i) {
        jQuery.ajax({
            type: "POST",
            url: server_url,
            data: JSON.stringify({
                "token": getCookie("token"),
                "command": "image_analysis",
                "object": object_name,
                "limit": batch
            }),
            success: function (data) {
                console.log(data);
                for (j = 0; j < data.length; j++) {
                    all_images.push(data[j]);
                }
                var percent_val = (i * 100 / max_iter).toFixed(0) + "%";
                $('#percent').text(percent_val);
                if (i < max_iter) {
                    request(i + 1);
                } else {
                    $('body').removeClass("processing");
                    display_images(all_images);
                    close_searching_window();
                }
            },
            error: function (x) {
                console.log(x);
                alert(x);
            },
            dataType: 'json'

        });
    }
    request(0);
    //alert("Find " + results.length + " manhole covers")
}

blobs = [];
filename = [];
function add_to_zip() {
    const toBlob = canvas => new Promise(resolve => canvas.toBlob(resolve));
    add_to_zip.task_item_num = add_to_zip.task_item_num || 0;
    var position = jQuery("#image").data("position");
    console.log(position);
    jQuery("#all_images").append("<tr><th>" + position.lat + "</th><th>" + position.long + "</th></tr>");
    close_image_window();
    blobs.push(toBlob($("#image")[0]));
    filename.push("lat-" + position.lat + "-long-" + position.long + ".png");
}

function download() {

    const toBlob = canvas => new Promise(resolve => canvas.toBlob(resolve));
    const createZipWriter = () => new Promise(resolve => zip.createWriter(new zip.BlobWriter(), resolve));
    const addFile = (zipWriter, name, blob) => new Promise(resolve => zipWriter.add(name, new zip.BlobReader(blob), resolve));
    const close = zipWriter => new Promise(resolve => zipWriter.close(resolve));
    var canvas = $("#image")[0];
    var position = jQuery.data(canvas, "position");
    let zip_writer;

    createZipWriter()
        .then(writer => {
            zip_writer = writer;
            return Promise.all(blobs);
        })
        .then(blobs => {
            const ret = [];
            let p = Promise.resolve();
            for (let i = 0; i < blobs.length; ++i) {
                p = p.then(() => {
                    return addFile(zip_writer, filename[i], blobs[i]);
                })
                    .then(x => ret.push(x));
            }
            return p;
        })
        .then(() => {
            return close(zip_writer);
        })
        .then(x => {

            var link = document.createElement('a');
            document.body.appendChild(link);
            link.href = URL.createObjectURL(x);
            link.download = "foo.zip";
            link.click();
            //$('#download')[0].download = "foo.zip";
            //$('#download')[0].href = URL.createObjectURL(x);
        });

    console.log('done');

}
