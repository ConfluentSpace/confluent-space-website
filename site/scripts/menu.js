document.addEventListener("DOMContentLoaded", function ()
{
    var toggle = document.getElementById("menu-toggle"),
            menu = document.getElementById("menu");

    toggle.addEventListener("mousedown", function (event)
    {
        event.preventDefault();
    });

    toggle.addEventListener("click", function (event)
    {
        event.preventDefault();
        menu.classList.toggle("open");

        if (window.getSelection)
        {
            window.getSelection().removeAllRanges();
        }
        else if (document.selection)
        {
            document.selection.empty();
        }
    });
});

document.onreadystatechange = function ()
{
    var toggle = document.getElementById("menu-toggle").firstElementChild;

    if (document.readyState === "complete")
    {
        if (window.getComputedStyle(toggle).fontFamily !== "FontAwesome")
        {
            document.body.classList.add("font-awesome-fallback");
        }
    }
};
