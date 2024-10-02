import React from 'react';
import './css/header.css'
import BlogPage from './blog_page'
import Header from './header'

function BlogHome(props){
    return(
        <div>
            <Header username={props.display.memberData.user.username}/>
            <BlogPage {...props}/>
        </div>
    )
}

export default BlogHome;