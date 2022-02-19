const init_scroll = () => {
    var element = document.getElementById('scroll-box');
    var bottom = element.scrollHeight - element.clientHeight;
    element.scroll(0, bottom);
}

const message_delete = () => {
    var result = window.confirm('メッセージを削除してもよろしいですか');
    if(result == true){
        pass;
    }else{
        return false;
    }
}