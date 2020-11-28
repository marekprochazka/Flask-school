
function copyToClipboard(id) {
    let button = document.getElementById(id);
    let copyText= button.textContent;
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