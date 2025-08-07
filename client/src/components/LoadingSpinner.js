import styled from "styled-components";

export default function LoadingSpinner() {
  return <Loading>Loading...</Loading>;
}

const Loading = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
`;
