import './css/notify.css'
import Request from './request'
import Utility from '../welcome_page/utility'

export default function Notification(props){


    //const requestList = []


    const requestList = props.display.memberData.request.map(request =>{
        return <Request  {...props} {...request} key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)}/>
    })


    return (
        <div className='notify'>
            <div className="notify-title">
                <button className="notify-button">
                    <div onClick={() =>Utility.changePage(props, 'home')}>go back</div>
                </button>
                <h1>Requests</h1>
            </div>
            {requestList}
        </div>
    )
}