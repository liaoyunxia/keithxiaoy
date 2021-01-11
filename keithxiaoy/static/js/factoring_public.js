$(function(){
	// 创建 datepicker
    $('.datepicker').datepicker({
        language: 'zh-CN',
        format: 'yyyy-mm-dd',
        autoHide: true,
    });
    // 绑定 pick.datepicker 事件
    $('.datepicker').on('pick.datepicker', function(e) {
        var $container = $(this).parent();
        if(e.date) {
            $container.addClass('is-dirty');
        } else {
            $container.removeClass('is-dirty');
        }
    });

    user_id = $('#login_user_id').attr('data-user_id') 
	if (user_id && user_id != 'None'){
		UpdateNotificationStatus(user_id);
	}
	
})

function insert_customer(uri, target){
	$.ajax({
		url: uri,
		type: 'GET',
		dataType: 'json',
	}).done(function(data) {
		var insert_html = ''; 
		for (ct in data['results']){
			obj = data['results'][ct];
			insert_html += mix('<option value="${id}">${name}</option>', {id: obj['id'], name: obj['name']})
		} 
		$(target).append(insert_html);
	})
	.fail(function(data) {
		if(data.status === 400){
			var err = JSON.parse(data.responseText).detail;
			alert(err)
		} else {
			alert('客户信息获取失败！');
		}
	});
}


function formatDateTime(d) {  
	  var D=['00','01','02','03','04','05','06','07','08','09']  
	  with (d || new Date) return [  
	    [getFullYear(), D[getMonth()+1]||getMonth()+1, D[getDate()]||getDate()].join('-'),  
	    //[D[getHours()]||getHours(), D[getMinutes()]||getMinutes(), D[getSeconds()]||getSeconds()].join(':')  
	  ]//.join(' ');  
	}  


function UpdateNotificationStatus(user_id){
	$.ajax({
		url: '/api/v1/users/'+user_id+'/notifications/status/',
		type: 'GET',
		dataType: 'json',
	})
	.done(function(data) {
		count = data['count']
		if(parseInt(count) > 0){
			$('#message_link').addClass('mdl-badge mdl-badge--overlap');
			$('#message_link').attr('data-badge', count);
		}else{
			$('#message_link').removeClass('mdl-badge mdl-badge--overlap');
		}
	})
	.fail(function() {
		alert('消息数据获取失败');return;
	});
}


function insert_diaries_results(diaries_results){
	insert_str = '<div class="mdl-steps__item mdl-steps--finish" onclick=\'go_vetting("${id}")\'>\
		<div class="mdl-steps__tail"></div>\
		<div class="mdl-steps__icon" style="background-color: #ffffff"></div>\
		<div class="mdl-steps__title">\
			<div class="mdl-grid" style="padding: 8px;">\
				<div class="mdl--cell mdl-cell--4-col-desktop mdl-cell--2-col-phone">${user_name}</div>\
				<div class="mdl--cell mdl-cell--8-col-desktop mdl-cell--2-col-phone">${created_time}</div>\
				<div class="mdl--cell mdl-cell--4-col-desktop mdl-cell--2-col-phone">${process_name}</div>\
				<div class="mdl--cell mdl-cell--8-col-desktop mdl-cell--2-col-phone" style="color:${vetting_result_color}; ">${vetting_result_message}</div>\
			</div>\
		</div>\
	</div>'
			
	var html = '' 
	for( i in diaries_results){
		item = diaries_results[i];
		var created_time = ''
		if(item.id != 0){
			var dateee = new Date(item.created_time).toJSON();  
			created_time = new Date(+new Date(dateee)+8*3600*1000).toISOString().replace(/T/g,' ').replace(/\.[\d]{3}Z/,'')
		}else{
			created_time = '&nbsp;'
		}
		html += mix(insert_str, {id: item.id, user_name: item.user.name, created_time: created_time, process_name: item.process_name,
			vetting_result_color: item.vetting_result.color, vetting_result_message: item.vetting_result.message, })
	}
	$('#diaries_result').html(html);
}


function GetData(href){
	var content = $('#list');
	$(event.target).addClass('is-active').siblings().removeClass('is-active');
	$.ajax({
			url: href,
			type: 'GET',
			dataType: 'json',
		})
		.done(function(data) {
			var source = $('#entry-template').html();
			var template = Handlebars.compile(source);
			content.html(template(data));
			$('#list').attr('data-endpoint', href);
		})
		.fail(function() {
			alert('数据获取失败');return;
		});
}

function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}
	
var imgs_list = new Array();  
function GetDateDiff(startTime, endTime, diffType) {
    //将xxxx-xx-xx的时间格式，转换为 xxxx/xx/xx的格式 
    startTime = startTime.replace(/\-/g, "/");
    endTime = endTime.replace(/\-/g, "/");

    //将计算间隔类性字符转换为小写
    diffType = diffType.toLowerCase();
    var sTime = new Date(startTime);      //开始时间
    var eTime = new Date(endTime);  //结束时间
    //作为除数的数字
    var divNum = 1;
    switch (diffType) {
        case "second":
            divNum = 1000;
            break;
        case "minute":
            divNum = 1000 * 60;
            break;
        case "hour":
            divNum = 1000 * 3600;
            break;
        case "day":
            divNum = 1000 * 3600 * 24;
            break;
        default:
            break;
    }
    return parseInt((eTime.getTime() - sTime.getTime()) / parseInt(divNum));
}


function go_vetting(url){
	if (parseInt(url)){
		location.href = '/vetting/'+url;
	}
}


function OnDropDownChange(dropDown) {
    var selectedValue = dropDown.options[dropDown.selectedIndex].value;
    $(dropDown).next().val(selectedValue)
}


!function(){
	Date.prototype.format = function (fmt) {
	    var o = {
	        "M+": this.getMonth() + 1, //月份 
	        "d+": this.getDate(), //日 
	        "h+": this.getHours(), //小时 
	        "m+": this.getMinutes(), //分 
	        "s+": this.getSeconds(), //秒 
	        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
	        "S": this.getMilliseconds() //毫秒 
	    };
	    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
	    for (var k in o)
	    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
	    return fmt;
	}
}


var upload_imgs = {}

function mix (str,group) {
	str = str.replace(/\$\{([^{}]+)\}/gm,function (m,n) {
		return (group[n] != undefined) ? group[n] : '';
	})
	return str;
}

function update_view(img_url, img_type){
	insert_html = '<div style="width:64px; height:64px; margin-right:5px; position:relative;display:inline-block;">'
				+ '<a href="${img_url}" data-fancybox>'
				+ '<img src=${img_url} style="width:64px; height:64px;"></a>'
				+ '<a href="#" class="mdl-color--grey-400" onclick="delect_images(\''+ img_url +'\', \''+img_type+'\', event)">'
				+ '<i class="material-icons" style="position:absolute;bottom:-1px;right:0;">cancel</i>'
				+ '</a>'
				+ '</div>'
	img_html = mix(insert_html, {img_url: img_url, img_type: img_type})
	$('#'+img_type+"_imgs").append(img_html)
	
	if (!upload_imgs.hasOwnProperty(img_type)){
		upload_imgs[img_type] = []
	}
	upload_imgs[img_type].push(img_url);
	var str = '';
	var index  = 0;
	
	for (img_url in upload_imgs[img_type]){
		str += upload_imgs[img_type][img_url];
		index += 1;
		if(index < upload_imgs[img_type].length){
			str += '|';
		}
	}
	$('input[name="'+img_type+'"]').val(str);
}

function delect_images(url, type, event){
	$(event.target).parent().parent().hide();
	
	var index = upload_imgs[type].indexOf(url);
	if (index > -1) {
		upload_imgs[type].splice(index, 1);
	}
	
	var str = ''
	for (img_url in upload_imgs[type]){
		str += upload_imgs[type][img_url];
		index += 1;
		if(index == upload_imgs.length){
			str += '|';
		}
	}
	$('input[name="'+type+'"]').val(str);
}


function outputmoney(number) {
	number = number.replace(/\,/g, "");
	if(isNaN(number) || number == "")return "";
	number = Math.round(number * 100) / 100;
	  if (number < 0)
	    return '-' + outputdollars(Math.floor(Math.abs(number) - 0) + '') + outputcents(Math.abs(number) - 0);
	  else
	    return outputdollars(Math.floor(number - 0) + '') + outputcents(number - 0);
	} 

//格式化金额
function outputdollars(number) {
  if (number.length <= 3)
    return (number == '' ? '0' : number);
  else {
    var mod = number.length % 3;
    var output = (mod == 0 ? '' : (number.substring(0, mod)));
    for (i = 0; i < Math.floor(number.length / 3); i++) {
      if ((mod == 0) && (i == 0))
        output += number.substring(mod + 3 * i, mod + 3 * i + 3);
      else
        output += ',' + number.substring(mod + 3 * i, mod + 3 * i + 3);
    }
    return (output);
  }
}

function outputcents(amount) {
	amount = Math.round(((amount) - Math.floor(amount)) * 100);
	return (amount < 10 ? '.0' + amount : '.' + amount);
}


var DateFormats = {
	       short: "YYYY-MMMM-DD ",
	       long: "dddd DD.MM.YYYY HH:mm"
	};
Handlebars.registerHelper("formatDate", function(datetime, format) {
	// Use UI.registerHelper..
	  if (moment) {
	    // can use other formats like 'lll' too
	    format = DateFormats[format] || format;
	    return moment(datetime).format(format);
	  }
	  else {
	    return datetime;
	  }
	});

Handlebars.registerHelper("splitLine", function(str_val, index) {
	return str_val.split("-")[index]
	});

Handlebars.registerHelper('ifCond', function(v1, v2, options) {
	  if(v1 === v2) {
	    return options.fn(this);
	  }
	  return options.inverse(this);
	});

Handlebars.registerHelper('chgMoney', function(v1, options) {
	 if(options == 1){
		 return outputmoney((v1/100.0).toString());
	 }else if (options == 10){
		 return parseInt(outputmoney((v1/10000/100).toString()));
	 }
	return v1;
	
	});


