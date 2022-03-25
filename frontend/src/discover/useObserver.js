import { useEffect, useRef, useState } from "react";

export default function useObserver( targetRef) {
    const [isIntersecting, setIsIntersecting] = useState(false);
    const observerRef = useRef(null);

    const options = {
        threshold: 0
    }

    useEffect(() => {
        observerRef.current = new IntersectionObserver(([entry]) => {
            setIsIntersecting(entry.isIntersecting);
        }, options);
    }, []);

    useEffect(() => {
        observerRef.current.observe(targetRef.current);

        return () => {
            observerRef.current.disconnect();
        };
    }, [targetRef]);

    return isIntersecting;
}
