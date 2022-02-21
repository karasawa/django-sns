const init_scroll = () => {
    var element = document.getElementById('scroll-box');
    var bottom = element.scrollHeight - element.clientHeight;
//    element.scroll(0, bottom);
    element.scrollTo({top: bottom, left: 0, behavior: 'smooth'});
}

const message_delete = () => {
//    const mini_menu = document.getElementById('mini_menu');
//    mini_menu.style.display = 'block';
    var result = window.confirm('メッセージを削除してもよろしいですか');
    if(result == true){
        pass;
    }else{
        return false;
    }
}

//const cancel = () => {
//    const mini_menu = document.getElementById('mini_menu');
//    mini_menu.style.display = 'none';
//    return false;
//}

const group_detail = () => {
    const target = document.getElementById('group_detail_menu');
    if(target.className == 'group_detail_menu'){
        const element = document.querySelector('.group_detail_menu');
        element.className = 'group_detail_menu_open';
    }else{
        const element = document.querySelector('.group_detail_menu_open');
        element.className = 'group_detail_menu';
    }
}

const close_menu = () => {
    const target = document.getElementById('group_detail_menu');
    if(target.className == 'group_detail_menu'){
        const element = document.querySelector('.group_detail_menu');
        element.className = 'group_detail_menu_open';
    }else{
        const element = document.querySelector('.group_detail_menu_open');
        element.className = 'group_detail_menu';
    }
}