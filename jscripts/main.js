function deleteStock(obj, sid){
	if(confirm('Are you sure to delete this stock?'))
	{
		$.get('/admin/deleteStock', {
		    sid: sid
		}, function() {
			$(obj).parents('tr:first').remove()
			$.jnotify("delete stock " + sid +" success.", true);
		    //alert('delete success!');
		});
	}
}

function addNewComment(sid){
	var c = $('input#comment'+ sid).val()
	$.post('/admin/addStockComment', {
	    stock_id: sid,
	    comment: c
	}, function() {
		$('#last_comment_td_'+sid).get(0).innerText=c
		$.jnotify("add new comment for " + sid +" success.", true);
	    //alert('add success!');
	});
}

function deleteAdminUser(){
	var n = $('input#adminUserName').val()
	if(!n || $.trim(n).length == 0){
	    alert("Error! nickname is null!")
	    return;
	}
	
	$.post('/admin/user/delete', {
	    name: n
	}, function() {
	    alert('delete success!');
	});
}

function addAdminUser(){
	var n = $('input#adminUserName').val()
	var p = $('input#adminUserPath').val()
	if(!n || $.trim(n).length == 0){
	    alert("Error! nickname is null!")
	    return;
	}
    if(!p || $.trim(p).length == 0){
        alert("Error! path is null!")
        return
    }
	$.post('/admin/user/add', {
	    name: n,
	    path: p
	}, function() {
	    alert('add success!');
	}, function(date){alert(date)});
}

function addStockCheck(){
	var value=$('#stock_value').val()
	if(/^\d+$/.test(value))
	{
		document.getElementById("newStockForm").submit()
		return true;
	}
	alert("stock id error!")
}

function changePage(obj){
	window.location.href="/?page=" + obj.options[obj.selectedIndex].value
}

function nextComment(sid, datetime){
	$.get('/admin/nextpage/'+sid+"/"+datetime, {}, function(data) {
		$('#last_comment_td_'+sid).get(0).innerText=""
		$('#last_comment_td_'+sid).append($(data))
	});
}
