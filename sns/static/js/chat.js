const init_scroll = () => {
    var element = document.getElementById('scroll-box');
    var bottom = element.scrollHeight - element.clientHeight;
    element.scroll(0, bottom);
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