import React from 'react';
import './css/header.css'
import BlogPage from './blog_page'
import Header from './header'

function BlogHome(){
    return(
        <div>
            <Header />
            <BlogPage />
        </div>
    )
}

export default BlogHome;