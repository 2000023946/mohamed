import Blog from './blog'
import Utility from '../welcome_page/utility'
export default function SearchResult(props){

    console.log(props)

    const handleClick = (props, blog) =>{
        Utility.handleClick(props, blog)
    }

    const searchList = props.display.memberData.search_data.map(blog =>{
        return  <Blog handleClick={() =>handleClick(props, blog)}  {...blog} key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)}/>
    })

    return(
        <div >
            <h1 >Results</h1>
            {searchList}
        </div>
    )
}