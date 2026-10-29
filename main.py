import streamlit as st
st.title('여누킴잡아먹기')
a=st.text_input('이름을 대시오')
b=st.selectbox('좋아하는 여누의 상태를 선택하세요',['화난 여누','예민한 여누','착해진 여누','우울한 여누', '행복한 여누'])
c=st.selectbox('여누를 어떻게 잡아먹을지 선택하세요',['정수리 물어뜯기','여누화나게해서훈제여누로만들어먹기','여누물에담가서삶아먹기'])
if st.button('여누야 인사하자'):
  st.write('어 하이?')
  st.info(a+' 문 닫고 들어와')
  st.warning(b+'인 상태를 좋아한다고? 미쳤구나?')
  st.error(c+' 이렇게 하고 나를 잡아먹겠다고? 맞을래?')
  st.bomb()
