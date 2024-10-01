import React, {useState} from 'react'
import BlogSection from './blog_section'
function BlogPage(){
    const name = ['Recommendation', 'Recents', "Popular", 'Your Blogs', 'All Blogs']
    const blogsList = name.map((title) =>{
       return(
            <BlogSection name={title} key={title}/>
        )
    })
    return(
        <div>
            {blogsList}
        </div>
    )
}

export default BlogPage;
