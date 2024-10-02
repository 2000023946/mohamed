
import Utility from './utility.js'

export default function Home(props){
    
    console.log(props)
    return(
        <div className="container">
            <div className="button-container">
                <h1 className="welcome-text">Welcome to BlogSpace</h1>
                <div>
                    <button onClick={() => Utility.handleClick(props.page.setPage, 'login')}>Login</button>
                </div>
                <div>
                    <button onClick={() => Utility.handleClick(props.page.setPage, 'signup')}>Sign up</button>
                </div>
            </div>
        </div>
    )
}