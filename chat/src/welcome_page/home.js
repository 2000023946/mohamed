
import Utility from './utility.js'

export default function Home(props){
    

    return(
        <div className="container">
            <div className="button-container">
                <h1 className="welcome-text">Welcome to BlogSpace</h1>
                <div>
                    <button onClick={() => Utility.handleClick(props, 'login')}>Login</button>
                </div>
                <div>
                    <button onClick={() => Utility.handleClick(props, 'signup')}>Sign up</button>
                </div>
            </div>
        </div>
    )
}