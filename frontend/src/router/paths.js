export default [
  {
    path: "",
    view: "Home",
    name: "home"
  },
  {
    path: "/search",
    view: "Search",
    name: "search"
  },
  {
    path: "/login",
    view: "Login",
    name: "login"
  },
  {
    path: "/signup",
    view: "Signup",
    name: "signup"
  },
  {
    path: "/list",
    view: "List",
    name: "list"
  },
  {
    path:"/searchlist/:keyword/:part",
    name:"Search",
    view: "MovieList"
  },
  {
    path:"/detail/:movieid/:part",
    name:"Detail",
    view: "MovieInfo"
  },
  {
    path: "/form",
    name: "Form",
    view: "Form"
  },
  {
    path: "/start",
    name: "Start",
    view: "Start"
  }
];

[

]