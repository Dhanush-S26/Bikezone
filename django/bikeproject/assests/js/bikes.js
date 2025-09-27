// Navigation Bar 
var bar = document.getElementById("bar")
var sidenavbar = document.getElementsByClassName("sidenavbar")[0]
function sideNavigationBar(){
    sidenavbar.style.display="block"
}
function closeSideNavigationBar(){
    sidenavbar.style.display="none"
}

// Load More Bikes
var bikes1 = document.getElementsByClassName("bikes1")[0]
var loadmore = document.getElementsByClassName("loadmore")[0]
function loadMoreBikes(){
    loadmore.style.display="none"
    bikes1.style.display="flex"
}

