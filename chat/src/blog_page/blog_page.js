import React, {useState} from 'react'
import BlogSection from './blog_section'
function BlogPage(props){
    const name = ['Recommendation', 'Recents', "Popular", 'Blogs']
    const blogsList = name.map((title) =>{
       return(
            <div key={title}>
                <h1>{title}</h1>
                <BlogSection type={title.toLowerCase()} {...props}/>
            </div>
        )
    })
    return(
        <div>
            {blogsList}
        </div>
    )
}

export default BlogPage;
