import React, { useState, useEffect, useContext } from 'react';
import { UserContext } from './context/UserContext';
import UserInfo from './UserInfo';
import UserSettings from './UserSettings';
import UserMessageList from './UserMessageList';

function UserProfile() {
  const { user } = useContext(UserContext);
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    // 假设有获取用户资料的 API
    const fetchUserInfo = async () => {
      const userDetails = await getUserInfo(user.id);
      setUserInfo(userDetails);
    };
    
    fetchUserInfo();
  }, [user]);

  if (!userInfo) return <div>Loading...</div>;

  return (
    <div>
      <UserInfo user={userInfo} />
      <UserSettings user={userInfo} />
      <UserMessageList userId={userInfo.id} />
    </div>
  );
}

export default UserProfile;
