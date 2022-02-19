const init_scroll = () => {
    var element = document.getElementById('scroll-box');
    var bottom = element.scrollHeight - element.clientHeight;
    element.scroll(0, bottom);
}