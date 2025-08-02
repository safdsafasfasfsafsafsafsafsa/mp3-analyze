import React from "react";
import styled from "styled-components";

export default function Footer() {
  const BASE_URL = "https://help.netflix.com/";

  return (
    <FooterContainer>
      <FooterContent>
        <FooterLinkContainer>
          <FooterLinkTitle>넷플릭스 대한민국</FooterLinkTitle>
          <FooterLinkContent>
            <FooterLink href={`${BASE_URL}/ko/node/412`}>
              넷플릭스 소개
            </FooterLink>
            <FooterLink href={`${BASE_URL}/ko/`}>고객 센터</FooterLink>
            <FooterLink href={`${BASE_URL}/ko/`}>미디어 센터</FooterLink>
            <FooterLink href={`${BASE_URL}/legal/termsofuse`}>
              이용약관
            </FooterLink>
            <FooterLink href={`${BASE_URL}/legal/privacy`}>개인정보</FooterLink>
            <FooterLink href={`${BASE_URL}/legal/corpinfo`}>
              회사정보
            </FooterLink>
            <FooterLink href={`${BASE_URL}/ko/contactus`}>문의하기</FooterLink>
            <FooterLink href={`${BASE_URL}/legal/notices`}>
              법적 고지
            </FooterLink>
          </FooterLinkContent>
          <FooterDescContainer>
            <FooterDescRights>Netflix Rights Reserved.</FooterDescRights>
          </FooterDescContainer>
        </FooterLinkContainer>
      </FooterContent>
    </FooterContainer>
  );
}

// 우선 가운데 정렬
const FooterContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
  border-top: 1px solid rgb(25, 25, 25);
  width: 100%;
  position: relative;
  z-index: 100;

  @media (max-width: 769px) {
    padding: 20px;
    padding-bottom: 30px;
  }
`;

// 통일성 위한 거라 별 내용 없음
const FooterContent = styled.div``;

const FooterLinkContainer = styled.div`
  width: 500px;

  @media (max-width: 768px) {
    width: 100%;
  }
`;

// 링크 목록 머리
const FooterLinkTitle = styled.h1`
  color: gray;
  font-size: 17px;
`;

// 링크 담는 공간
const FooterLinkContent = styled.div`
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-top: 35px;

  @media (max-width: 768px) {
    margin-top: 26px;
  }
`;

// 링크
const FooterLink = styled.a`
  color: gray;
  font-size: 14px;
  width: 110px; // 전체 너비 500에서 110 사용 -> 4번 쓰면 다음 줄로 이동
  margin-bottom: 21px; // 줄 간격
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }

  @media (max-width: 768px) {
    margin-bottom: 16px;
  }
`;

// 저작권 표기
const FooterDescContainer = styled.div`
  margin-top: 30px;

  @media (max-width: 768px) {
    margin-top: 20px;
  }
`;

const FooterDescRights = styled.h2`
  color: white;
  font-size: 14px;
  text-align: center;
`;
