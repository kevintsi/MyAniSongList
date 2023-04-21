import { useRouter } from 'next/router'

const Posts = () => {
    const router = useRouter()
    const { id } = router.query

    return <p>Post: {id}</p>
}

export default Posts