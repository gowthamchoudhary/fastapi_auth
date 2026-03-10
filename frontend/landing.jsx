import React from 'react'
import loginpage from './loginpage' 
import register from './register'
const login = () => {
    display = None
  return (
    <>
    <div className='Main-title'>
        <button onClick={()=>{display=true}}>Login</button> {"or"} <div onClick={()=>{display=false}}>Register</div>
        display?{
          <loginpage></loginpage>
        }:{
          <register></register>
        }
    </div>
    </>
  )
}

export default login  