function box_1_hover() {
    document.getElementsByClassName('host-box')[0].style.width = '100%';
    document.getElementsByClassName('join-box')[0].style.width = '0';
    document.getElementById('join-text-box').style.opacity = '0';
}

function box_2_hover() {

    document.getElementById('host-text-box').style.opacity = '1';
    document.getElementById('join-text-box').style.opacity = '1';
    document.getElementsByClassName('host-box')[0].style.width = '50%';
    document.getElementsByClassName('join-box')[0].style.width = '50%';
}

function box_3_hover() {
    document.getElementById('host-text-box').style.opacity = '0';
    document.getElementsByClassName('host-box')[0].style.width = '0';
    document.getElementsByClassName('join-box')[0].style.width = '100%';
}