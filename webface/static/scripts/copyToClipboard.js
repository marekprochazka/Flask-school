
function copyToClipboard(id) {
    let button = document.getElementById(id);
    let shortcut = button.textContent;
    let url = window.location.href;
    let copyText = url+shortcut;
    const el = document.createElement('textarea');
    el.value = copyText;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    alert(`Adresa: ${copyText} byla zkopírována do schránky!`)
    
    
}