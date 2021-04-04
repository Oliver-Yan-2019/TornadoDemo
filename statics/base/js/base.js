const pathname = window.location.pathname;
if (pathname.startsWith('/home')) {
    $('#HeaderNavHome').addClass('active');
} else if (pathname.startsWith('/article')) {
    $('#HeaderNavArticle').addClass('active');
}