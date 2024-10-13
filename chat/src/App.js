
import React, {useState, useEffect} from 'react';
import WelcomePage from './welcome_page/welcome_page';
import BlogHome from './blog_page/blog_home'
import Utility from './welcome_page/utility';


function App() {
      
  const [display, setDisplay] = useState({
    'name':'WelcomePage',
    'main':'',
    'memberData':{},
    'error':'',
  })

  const [page, setPage] = useState('home');

  const data={
    'display':{
      ...display,
      'setDisplay':setDisplay
    },
    'page':{
      'name':page,
      'setPage':setPage
    }
  }

  Utility.useUpdateHistory(data.page.setPage)
  console.log(data)

  //reconfigure url links upon reload
  if (display.name==='WelcomePage' && !(['home', 'signup', 'login'].includes(page))){
    setDisplay((oldDisplay) => {
      return {
        'memberData':JSON.parse(localStorage.getItem('user')),
        'name':'BlogHome',
        'main':'home',
        'error':'',
      }
    })
  }
  if (display.name === 'BlogHome' && (['home', 'signup', 'login'].includes(page))){
    setDisplay({
      'name':'WelcomePage',
      'main':'',
      'memberData':{},
      'error':'',
    })
  }

  

  return(
    <div>
      {display.name === 'BlogHome' && <BlogHome {...data}/>}
      {display.name === 'WelcomePage' && <WelcomePage {...data}/>}
    </div>
  )
}

export default App;
