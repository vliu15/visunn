/**
 * @file component that wraps canvas (for sizing)
 * @author Vincent Liu
 */

import styled from 'styled-components';


const CanvasContainer = styled.div`
    position: absolute;
    max-height: calc(100vh - 50px);
    min-width: 100vw;
    width: 100%;
    height: 100%;
`

export default CanvasContainer;
