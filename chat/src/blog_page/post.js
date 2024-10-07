import './css/blog_post.css'
import Utility from '../welcome_page/utility'
export default function Post(props){
    return(
        <div className="post-message">
            <p> {props.username} </p><br/>
            <p> {props.txt_message} </p><br/>
            <p> {props.date} </p>
            <div className = "post-remove-button">remove</div>
            <div className = "post-update-button">update</div>
        </div>
    )
}