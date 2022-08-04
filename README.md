<h3 align="center"><b>▪그 웹툰 어때▪</b></h3>

<h4 align="center">1주차 프로젝트(6조)</h4>
<br>


<h3 align="center"><b>📎 로고와 설명 </b></h3>

<table>
    <tr>
        <td width="20%" length="20%"><img src="https://user-images.githubusercontent.com/110237141/182097429-1334fcbb-4263-46b9-87d6-548f885e80b1.png" /></td>
    </tr>
    <td>
        <h5> '그 웹툰 어때'는 네이버 웹툰 중 개그 웹툰에 대한 리뷰와 별점을 공유하는 웹 어플입니다 </h5>
    </td>
    
</table>


<h3 align="center"><b>📎 와이어 프레임 및  </b></h3>
<br>
<h4><b>🔎 로그인페이지 </b></h4>

<table width="100%">
    <tr>
        <td width="50%"><img src="https://user-images.githubusercontent.com/110237141/182098738-06b148f7-fc91-40bc-a6b9-7e886da8d314.jpg" /></td>
        <td width="50%">
            <h5>로그인</h5>
            <ul>
                <li>______</li>
                <li>______</li>
            </ul>
        </td>
    </tr>
</table>

<h4><b>🔎 회원가입페이지 </b></h4>

<table width="100%">
    <tr>
        <td width="50%"><img src="https://user-images.githubusercontent.com/110237141/182112578-277e1331-7d71-45c9-8e26-20f08937fd99.png" /></td>
        <td width="50%">
            <h5>회원가입</h5>
            <ul>
                <li>______</li>
                <li>______</li>
            </ul>
        </td>
    </tr>
</table>

<h4><b>🔎 메인페이지 </b></h4>

<table width="100%">
    <tr>
        <td width="50%"><img src=https://user-images.githubusercontent.com/110237141/182099314-e7b13364-3175-4d4b-a69e-d99e98cc23c8.png /></td>
        <td width="50%">
            <h5>웹툰 목록</h5>
            <ul>
	     <li> 실제 네이버 개그웹툰의 정보를 크롤링</li>  
	     <li> 해당 웹툰 클릭시 클릭한 div의 정보를 SesionStorage에 저장</li>
            </ul>
        </td>
    </tr>
</table>

<h4><b>🔎 리뷰페이지 </b></h4>

<table width="100%">
    <tr>
        <td width="50%"><img src=https://user-images.githubusercontent.com/110237141/182099511-175c5d77-479f-41b6-8465-397d11f3e5d2.jpg /></td>
        <td width="50%">
            <h5>리뷰</h5>
            <ul>
	     <li> 저장한 div의 정보를 기반으로 해당웹툰 고유의 리뷰페이지 출력</li>  
	     <li> 웹툰에 대한 편리한 리뷰 등록/삭제</li>  
            </ul>
        </td>
    </tr>
</table>

<h4><b>🔎 마이페이지 </b></h4>

<table width="100%">
    <tr>
        <td width="50%"><img src= /></td>
        <td width="50%">
            <h5>리뷰</h5>
            <ul>
	     <li> 개인 ID와 리뷰에 대한 정보를 확인</li>  
	     <li> 비밀번호 변경과 회원 탈퇴기능</li>
            </ul>
        </td>
    </tr>
</table>

<h4><b>🔎 마이페이지 </b></h4>

<table width="100%">
    <tr>
        <td width="50%"><img src= /></td>
        <td width="50%">
            <h5>리뷰</h5>
            <ul>
	    <li> 리뷰페이지와 달리 자신이 작성한 모든 리뷰 열람 </li>  
            </ul>
        </td>
    </tr>
</table>

<br>
<h3 align="center"><b>🏷 API Table 🏷</b></h3>
<table width="100%">
    <tr align="center">
	<td width="12%"><b>Function</b></td>
        <td width="5%"><b>Method</b></td>
        <td width="12%"><b>URL</b></td>
        <td width="30%"><b>Request</b></td>
        <td width="31%"><b>Response</b></td>
    </tr>
    <tr>
        <td width="12%">메인화면 페이지 로드</td>
        <td width="5%"></td>
        <td width="12%">/</td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">로그인 페이지 로드</td>
        <td width="5%"></td>
        <td width="12%">/</td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">회원가입 페이지 로드</td>
        <td width="5%"></td>
        <td width="12%">/</td>
        <td width="30%"></td>
        <td width="31%"</td>
    </tr>
    <tr>
        <td width="12%">글쓰기 페이지 로드</td>
        <td width="5%"></td>
        <td width="12%"></td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">회원가입</td>
        <td width="5%"></td>
        <td width="12%"></td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">ID 중복검사</td>
        <td width="5%"></td>
        <td width="12%"></td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">로그인</td>
        <td width="5%"></td>
        <td width="12%"></td>
        <td width="30%">{'id': username_give, 'pw': password_give}</td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">리뷰 저장</td>
        <td width="5%">POST</td>
        <td width="12%"></td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">개인 페이지 로드</td>
        <td width="5%"></td>
        <td width="12%"></td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">개인정보 수정 삭제</td>
        <td width="5%"></td>
        <td width="12%"></td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>

</table>

<br>
