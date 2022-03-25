import { useEffect, useRef, useState } from "react";

export default function useObserver( targetRef) {
    const [isIntersecting, setIsIntersecting] = useState(false);
    const observerRef = useRef(null);

    const options = {
        threshold: 0
    }

    useEffect(() => {
        console.log("creating new intersection observer");
        observerRef.current = new IntersectionObserver(([entry]) => {
            console.log(entry);
            setIsIntersecting(entry.isIntersecting);
        }, options);
    }, []);

    useEffect(() => {
        console.log("targetRef", targetRef);
        observerRef.current.observe(targetRef.current);

        return () => {
            observerRef.current.disconnect();
        };
    }, [targetRef]);

    return isIntersecting;
}
