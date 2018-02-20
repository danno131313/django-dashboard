$(document).ready(function() {
    $('.ui.dropdown').dropdown();
    $('.delete').click(function() {
        user_id = $(this).val();
        document.getElementById('modal').innerHTML = "\
            <div id='user" + user_id + "' class='ui basic modal'>\
                <div class='ui header'>\
                    Delete User " + user_id + "\
                </div>\
                <div class='content'>\
                    <p>Are you sure you want to delete user " + user_id + "?</p>\
                </div>\
                <div class='actions'>\
                    <div class='ui blue inverted cancel button'>\
                        <i class='remove icon'></i>\
                        No\
                    </div>\
                    <a href='/users/" + user_id + "/delete' class='ui red inverted button'>\
                        <i class='checkmark icon'></i>\
                        Yes\
                    </a>\
                </div>\
            </div>\
            ";
        $('#user' + user_id).modal('show');
    });
});
