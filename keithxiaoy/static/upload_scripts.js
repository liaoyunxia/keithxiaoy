(function(){
    'use strict'

    var getCookie = function(name) {
        var value = '; ' + document.cookie,
            parts = value.split('; ' + name + '=')
        if (parts.length == 2) return parts.pop().split(';').shift()
    }
    
    var jic = {
        compress : function(source_img_obj, quality, output_format) {

            var mime_type = "image/jpeg";
            if (output_format != undefined && output_format == "png") {
                mime_type = "image/png";
            }
            var rate = source_img_obj.width / source_img_obj.height;
            var cvs = document.createElement('canvas');
            // naturalWidth真实图片的宽度
            cvs.width = Math.sqrt(1300000*rate);
            cvs.height = cvs.width / rate;
            cvs.style.border = '0px';
            var ctx = cvs.getContext("2d");
            ctx.drawImage(source_img_obj, 0, 0, cvs.width, cvs.height);
            var newImageData = cvs.toDataURL(mime_type, quality / 100);
            var binary = atob(newImageData.split(',')[1]);
            var buffer = new Uint8Array(binary.length);
            for (var i = 0; i < binary.length; i++) {
                buffer[i] = binary.charCodeAt(i);
            }
            var blob = new Blob([buffer.buffer], {type: 'image/jpeg'});
            blob['Content-Type'] = 'image/jpeg';
            return blob;
        },
    }
    function fileToCanvas(file, data, el) {
        if (!file.type.match('image.*')) {
            alert("请选择图片");
        }
        var reader = new FileReader();
        // Closure to capture the file information.
        reader.onload = (function(theFile, data, el) {
            return function(e) {
                var image = new Image();
                image.src = e.target.result;
                var quality = 80;
                var blob = jic.compress(image, quality, '');
                upload(blob, data, el)
            };
        })(file, data, el);
        reader.readAsDataURL(file);
    }
    // end
    var request = function(method, url, data, headers, el, showProgress, cb) {
        var req = new XMLHttpRequest()
        req.open(method, url, true)
        Object.keys(headers).forEach(function(key){
            req.setRequestHeader(key, headers[key])
        })
        
        req.onload = function() {
            cb(req.status, req.responseText);
        }

        req.onerror = req.onabort = function() {
            disableSubmit(false);
            error(el, 'Sorry, failed to upload file.')
        }
        req.upload.onprogress = function(data) {
            progressBar(el, data, showProgress);
        }

        req.send(data)
    }

    var parseURL = function(text) {
        var xml = new DOMParser().parseFromString(text, 'text/xml'),
            tag = xml.getElementsByTagName('Location')[0],
            url = unescape(tag.childNodes[0].nodeValue)

        return url
    }

    var parseJson = function(json) {
        var data
        try {data = JSON.parse(json)}
        catch(e){ data = null }
        return data
    }

    var progressBar = function(el, data, showProgress) {
        if(data.lengthComputable === false || showProgress === false) return

        var pcnt = Math.round(data.loaded * 100 / data.total),
            bar  = el.querySelector('.bar')

        bar.style.width = pcnt + '%'
    }

    var error = function(el, msg) {
        el.className = 's3direct form-active'
        el.querySelector('.file-input').value = ''
        alert(msg)
    }
    
    var update = function(el, data) {
        var link = el.querySelector('.file-link'),
            url  = el.querySelector('.file-url')

        url.value = data['domain'] + data['key']
        var e_type = el.getAttribute('data-imgtype')
        update_view(url.value, e_type);
        
//        link.setAttribute('src', url.value)
//        link.innerHTML = url.value.split('/').pop()

        el.className = 's3direct link-active'
        el.querySelector('.bar').style.width = '0%'
    }

    var concurrentUploads = 0
    var disableSubmit = function(status) {
        var submitRow = document.querySelector('.submit-row')
        if( ! submitRow) return

        var buttons = submitRow.querySelectorAll('input[type=submit]')

        if (status === true) concurrentUploads++
        else concurrentUploads--

        ;[].forEach.call(buttons, function(el){
            el.disabled = (concurrentUploads !== 0)
        })
    }

    var upload = function(file, data, el) {
        var form = new FormData()

        disableSubmit(true)

        if (data === null) return error(el, 'Sorry, could not get upload URL.')

        el.className = 's3direct progress-active'
        var url  = data['domain']
        delete data['form_action']

        Object.keys(data).forEach(function(key){
            form.append(key, data[key])
        })
        form.append('file', file);
        $.ajax({
            type:"POST",
            url:url,
            data: form,
            processData: false,
            contentType: false,
            
        }).done(function(res) {
            disableSubmit(false)
            update(el, data);
            
        }).fail(function(res) {
            alert('图片上传失败');
            disableSubmit(false)

        });
//        request('POST', url, form, {}, el, true, function(status, xml){
//            disableSubmit(false)
//            console.log(status)
//            if(status !== 204) return error(el, 'Sorry, failed to upload to S3.')
//            update(el, xml, data)
//        })
    }
    

    var getUploadData = function(e) {
        var el       = e.target.parentElement,
            file     = el.querySelector('.file-input').files[0],
            url      = el.getAttribute('data-policy-url'),
            headers  = {'X-CSRFToken': getCookie('csrftoken'), 'Accept': 'application/json'};
        if(file.size < 700 * 1024) {
            var url = url + '&filename=' + file.name;
        } else {
            var url = url + '&filename=' + file.name + '.jpg';
        }
        request('GET', url, null, headers, el, false, function(status, json){
            var data = parseJson(json);
            switch(status) {
                case 200:
                    upload(file, data, el);
                    break
                case 400:
                    alert("400cuowu");
                case 403:
                    error(el, data.error)
                    break;
                default:
                    error(el, 'Sorry, could not get upload URL.')
            }
        })
    }

    var removeUpload = function(e) {
        e.preventDefault()

        var el = e.target.parentElement
        el.querySelector('.file-url').value = ''
        el.querySelector('.file-input').value = ''
        el.className = 's3direct form-active'
    }

    var addHandlers = function(el) {
        var url    = el.querySelector('.file-url'),
            input  = el.querySelector('.file-input'),
            remove = el.querySelector('.file-remove'),
            status = (url.value === '') ? 'form' : 'link'

        el.className = 's3direct ' + status + '-active'

        remove.addEventListener('click', removeUpload, false)
        input.addEventListener('change', getUploadData, false)
    }

    document.addEventListener('DOMContentLoaded', function(e) {
        ;[].forEach.call(document.querySelectorAll('.s3direct'), addHandlers)
    })

    document.addEventListener('DOMNodeInserted', function(e){
        if(e.target.tagName) {
            var el = e.target.querySelector('.s3direct')
            if(el) addHandlers(el)
        }
    })

})()
