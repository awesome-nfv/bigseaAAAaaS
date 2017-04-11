var source = 'https://eubrabigsea.dei.uc.pt/web/manage_info_auth'

$(function() {
    $('#error').hide();
    $('#success').hide();
    window.addEventListener("message", postMessageHandler, false);
    //window.addEventListener('message', function(event) {
    //  alert(`Received ${event.data} from ${event.origin}`);
    //});

    $( "#btn_save" ).click(function() {
        console.log('clickSave');
	var f = $('#updateform');
	f.parsley().validate();
	if (f.parsley().isValid()) {
		console.log('data input is valid. proceed to submit form and update records');
		updateInfo();
	} else {
		console.log('data validation failed');
	}
    });

    $( "#btn_delete" ).click(function() {
        console.log('clickDelete');
	var f = $('#updateform');
        f.parsley().validate();
        if (f.parsley().isValid()) {
                console.log('data input is valid. proceed to submit form and delete account');
                deleteAccount();
        } else {
                console.log('data validation failed');
        }
    });
});



function postMessageHandler( event ) {
	console.log("Received info from user to update data.");
  	console.log("* Message:", event.data);
  	console.log("* Origin:", event.origin);
  	console.log("* Source:", event.source);

	$('#user').val(event.data.user_info.user.username)
	$('#email').val(event.data.user_info.user.email)
	$('#fname').val(event.data.user_info.user.fname)
	$('#lname').val(event.data.user_info.user.lname)
	$('#token').val(event.data.user_info.user_token)

	// check request is from legitimate source and message is expected or not
  	if ( event.origin !== source ) { return; }
    	// give response
    	//in case I want to send a reply to auth page, do it here
	// but handle the response there
	//event.source.postMessage( 'response', 'http://eubrabigsea.dei.uc.pt/web/manage_info_auth' );
    	}




function updateInfo(){
    $.ajax({
        url: '/engine/api/update_user',
        type: 'post',
        data: {'user': $('#user').val(), 'pwd': $('#pwd').val(), 'fname': $('#fname').val(), 'lname': $('#lname').val(), 'email': $('#email').val()},
        success: function (result) {
	    view_data = result;
	    console.log(result);
            console.log(result['error']);
	    error = result['error'];
            if (error) {
		//alert(error);
		$('#success').text('');
		$('#success').hide();
		$('#error').text(error);
		$('#error').show();
            } else {
		msg = "Updated with success!";
		$('#error').text('');
		$('#error').hide();
		$('#success').text(msg);
		$('#success').show();
	    }
        }
    });
}

function checkDelete(){
    return confirm('Are you sure you want to delete your account?');
}

function deleteAccount(){
    $.ajax({
        url: '/engine/api/delete_user',
        type: 'post',
        //data: {'user': $('#user').val(), 'pwd': $('#pwd').val(), 'fname': $('#fname').val(), 'lname': $('#lname').val(), 'email': $('#email').val()},
        data: {'user': $('#user').val(), 'token': $('#token').val()},
	success: function (result) {
            view_data = result;
            console.log(result);
            console.log(result['error']);
            error = result['error'];
            if (error) {
                //alert(error);
                $('#success').text('');
                $('#success').hide();
                $('#error').text(error);
                $('#error').show();
            } else {
                msg = "Account permanently deleted!";
                $('#error').text('');
                $('#error').hide();
                $('#success').text(msg);
                $('#success').show();
            }
        }
    });
}
