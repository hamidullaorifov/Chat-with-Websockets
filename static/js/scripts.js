let newContacts =document.querySelector('#contacts');
let search =document.querySelector('#search-input');
search.addEventListener('keyup',function(){
    let q = search.value;
    $.ajax({
        url: "/get_users?q=" + q,
        type: "GET",
        success: function (response) {
            if (q.trim()==''){
                window.location='/'
            }
            let users = response['users']
            let htmltext = ''
            for(let i=0;i<users.length;i++){
                htmltext+=create_contect(users[i]['fullname'],users[i]['id'])
            }
            newContacts.innerHTML = htmltext;
            // $('#contacts').html(response);
        }
    });
})

function create_contect(user,id){
    let element = `<a href="/${id}" class="user list-group-item data-userid=${id}
    list-group-item-action border-0">
    <div class="d-flex align-items-start">
        <img
            src="https://globalsurgery.med.ubc.ca/files/2022/08/default.jpg"
            class="rounded-circle mr-1" alt="" width="40" height="40">
        <div class="flex-grow-1 ml-3">
        ${user}
            <div class="small">
                <span class="fas fa-circle
                    chat-online"></span>
                Online
            </div>
        </div>
    </div>
</a>`

 return element
}

// let users = document.querySelectorAll('.user');
// for(let user in users){
//     user.addEventListener('click',function(){

//     })
// }